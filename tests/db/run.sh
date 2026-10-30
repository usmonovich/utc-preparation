#!/usr/bin/env bash
# Проверка миграций и RLS на настоящем Postgres 16 (без Docker): initdb во временной папке.
set -euo pipefail
cd "$(dirname "$0")/../.."
PG=/usr/lib/postgresql/16/bin
DIR=$(mktemp -d); PORT=55432
chown -R postgres "$DIR" 2>/dev/null || true
run() { if [ "$(id -u)" = 0 ]; then su postgres -c "$*"; else bash -c "$*"; fi; }
run "$PG/initdb -D $DIR/data -U postgres >/dev/null"
run "$PG/pg_ctl -D $DIR/data -o '-p $PORT -k $DIR' -l $DIR/log start >/dev/null"
trap 'run "$PG/pg_ctl -D $DIR/data stop -m fast >/dev/null"; rm -rf $DIR' EXIT
sleep 1
PSQL="$PG/psql -h $DIR -p $PORT -U postgres -d postgres -q -X"
# пакет: утверждаем два вопроса, как сделал бы администратор
node -e "const p=require('./content/pack.json');p.questions[0].status='approved';p.questions[1].status='approved';require('fs').writeFileSync('$DIR/pack.json',JSON.stringify(p))"
chmod 644 $DIR/pack.json; cp $DIR/pack.json /tmp/fpk_pack.json; chmod 644 /tmp/fpk_pack.json
run "$PSQL -f tests/db/auth-stub.sql"
run "$PSQL -v ON_ERROR_STOP=1 -f supabase/migrations/0001_schema.sql"
run "$PSQL -c \"create table public.tmp_pack(p jsonb); copy public.tmp_pack from '/tmp/fpk_pack.json' with (format csv, quote E'\\\\x01', delimiter E'\\\\x02'); grant select on public.tmp_pack to authenticated, anon;\"" >/dev/null
run "$PSQL -f tests/db/rls-test.sql"
run "$PSQL -f tests/db/rls-test2.sql"
# миграция 0002 (второй предмет) поверх базы с опубликованной физикой; повторный запуск безопасен
run "$PSQL -v ON_ERROR_STOP=1 -f supabase/migrations/0002_subjects.sql"
run "$PSQL -v ON_ERROR_STOP=1 -f supabase/migrations/0002_subjects.sql"
node -e "const p=require('./content/math/pack.json');p.questions[0].status='approved';require('fs').writeFileSync('$DIR/math.json',JSON.stringify(p))"
chmod 644 $DIR/math.json; cp $DIR/math.json /tmp/fpk_math.json; chmod 644 /tmp/fpk_math.json
run "$PSQL -c \"create table public.tmp_math_pack(p jsonb); copy public.tmp_math_pack from '/tmp/fpk_math.json' with (format csv, quote E'\\\\x01', delimiter E'\\\\x02'); grant select on public.tmp_math_pack to authenticated;\"" >/dev/null
run "$PSQL -c \"insert into auth.users values ('00000000-0000-0000-0000-00000000000c', 'student2@example.com');\"" >/dev/null
run "$PSQL -f tests/db/subjects-test.sql"
