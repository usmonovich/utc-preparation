// Стартовый экран UTC Preparation: выбор предмета. У каждого предмета — свой прогресс и своя учебная база.

import { indexOf, lastSubject, runtimes, useStore } from '../../data/store';
import { SUBJECTS, SUBJECT_IDS, APP_TITLE, type SubjectId } from '../../data/subjects';
import { overview } from '../../domain/progress';
import { Icon } from '../components/Icon';
import { Progress, plural } from '../components/ui';
import { href, navigate } from '../router';

function SubjectCard({ id }: { id: SubjectId }) {
  const meta = SUBJECTS[id];
  const user = useStore(runtimes[id].userStore);
  useStore(runtimes[id].adminStore);
  const idx = indexOf(id);
  const ov = overview(user, idx);
  const ready = ov.topicsTotal > 0;
  return (
    <a
      href={href('', id)}
      className={`subject-card subject-${id}`}
      onClick={(e) => {
        if (e.metaKey || e.ctrlKey || e.shiftKey) return;
        e.preventDefault();
        navigate('', { subject: id });
      }}
    >
      <span className="subject-icon" aria-hidden="true"><Icon name={meta.icon} size={34} /></span>
      <span className="subject-text">
        <b>{meta.title}</b>
        <span>{meta.tagline}</span>
      </span>
      <Icon name="next" />
      <span className="subject-stats">
        {ready ? (
          <>
            <span>{ov.topicsTotal} {plural(ov.topicsTotal, 'тема', 'темы', 'тем')} · изучено {ov.topicsStudied}</span>
            <Progress value={ov.percentStudied} label={`${meta.title}: изучено тем`} tone="accent" />
          </>
        ) : (
          <span>курс готовится</span>
        )}
      </span>
    </a>
  );
}

export function StartScreen() {
  const last = lastSubject();
  return (
    <div className="screen start">
      <header className="hero">
        <p className="eyebrow">Подготовка к вступительному экзамену</p>
        <h1>{APP_TITLE}</h1>
        <p className="muted">Выберите предмет. Прогресс, тесты и избранное у каждого предмета свои.</p>
      </header>
      <nav className="subject-list" aria-label="Предметы">
        {SUBJECT_IDS.map((id) => <SubjectCard key={id} id={id} />)}
      </nav>
      {last ? (
        <p className="start-last muted small">
          В прошлый раз: <a href={href('', last)}>{SUBJECTS[last].title}</a>
        </p>
      ) : null}
      <p className="start-foot small">
        <a href={href('settings', last ?? 'physics')}><Icon name="gear" size={16} /> Настройки</a>
      </p>
    </div>
  );
}
