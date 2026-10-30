\set ON_ERROR_STOP on
-- Миграция 0002 поверх базы, где уже опубликована физика: данные физики сохраняются, математика публикуется отдельно.
create temp table before_m as
  select (select count(*) from public.questions) q, (select count(*) from public.theories) t, (select count(*) from public.topics) tp,
         (select count(*) from public.content_versions) v;
select (select count(*) from public.sections where subject = 'physics') = (select count(*) from public.sections) as "после 0002 все прежние разделы — физика";
select (select count(*) from public.content_versions where subject = 'physics') = (select count(*) from public.content_versions) as "прежние версии помечены как физика";

-- администратор публикует математику
set role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000a', false);
select public.publish_content_pack((select p from public.tmp_math_pack)) as "опубликована версия математики";
-- студент не может публиковать и математику
select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000c', false);
do $$ begin perform public.publish_content_pack((select p from public.tmp_math_pack)); raise exception 'FAIL: студент опубликовал математику'; exception when insufficient_privilege then raise notice 'OK: студенту публикация математики запрещена'; end $$;
reset role;

do $$
declare b record;
begin
  select * into b from before_m;
  if (select count(*) from public.questions where id not like 'ma-%') <> b.q then raise exception 'FAIL: изменилось число вопросов физики'; end if;
  if (select count(*) from public.theories where id not like 'ma-%') <> b.t then raise exception 'FAIL: изменилось число блоков теории физики'; end if;
  if (select count(*) from public.topics where id not like 'ma-%') <> b.tp then raise exception 'FAIL: изменилось число тем физики'; end if;
  if (select count(*) from public.sections where subject = 'math') <> 2 then raise exception 'FAIL: разделы математики не помечены'; end if;
  if (select count(*) from public.sections where subject = 'physics' and id like 'ma-%') > 0 then raise exception 'FAIL: раздел математики помечен как физика'; end if;
  if (select count(*) from public.content_versions where subject = 'math') <> 1 then raise exception 'FAIL: нет версии математики'; end if;
  if (select count(*) from public.content_versions where subject = 'physics') <> b.v then raise exception 'FAIL: изменились версии физики'; end if;
  if (select count(*) from public.questions where id like 'ma-%') = 0 then raise exception 'FAIL: вопросы математики не опубликованы'; end if;
  raise notice 'OK: физика не изменилась, математика опубликована отдельно';
end $$;

-- приложение физики берёт последнюю версию своего предмета, а не математики
select (select pack -> 'course' ->> 'id' from public.content_versions where subject = 'physics' order by published_at desc limit 1) = 'physics' as "последняя версия физики — физика",
       (select pack -> 'course' ->> 'id' from public.content_versions where subject = 'math' order by published_at desc limit 1) = 'math' as "версия математики — математика";

-- прогресс по математике хранится в тех же таблицах и виден только владельцу
set role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000c', false);
insert into public.user_progress (user_id, topic_id, studied_at) values (auth.uid(), 'ma-1-1-1', now()), (auth.uid(), 'kin-basics', now());
select count(*) filter (where topic_id like 'ma-%') as "тем математики у студента", count(*) filter (where topic_id not like 'ma-%') as "тем физики у студента" from public.user_progress;
reset role;
