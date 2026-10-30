// Предметы приложения UTC Preparation. У каждого предмета своя учебная база (pack), свой прогресс
// ученика и свои решения проверки: данные физики и математики не смешиваются.
// Ключи хранилища и документы базы артефакта у физики остались прежними — сохранённые данные не теряются.

export type SubjectId = 'physics' | 'math';

/** Слова интерфейса, которые зависят от источника предмета: у физики — конспект, у математики — книга. */
export interface Vocab {
  src: string; // конспект / книга
  ofSrc: string; // конспекта / книги
  inSrc: string; // в конспекте / в книге
  toSrc: string; // к конспекту / к книге
  fromSrc: string; // из конспекта / из книги
  bySrc: string; // по конспекту / по книге
  allSections: string;
}

export interface SubjectMeta {
  id: SubjectId;
  /** Первый сегмент адреса: #/p/… — физика, #/m/… — математика. */
  prefix: 'p' | 'm';
  title: string;
  tagline: string;
  icon: 'atom' | 'pi';
  storage: { user: string; admin: string; pack?: string };
  cloud: { admin: string; user: (uid: string) => string };
  exportKind: string;
  /** В математике весь материал составлен по открытым источникам — отдельная пометка «из интернета» не нужна. */
  webIsDefault: boolean;
  v: Vocab;
}

export const SUBJECTS: Record<SubjectId, SubjectMeta> = {
  physics: {
    id: 'physics',
    prefix: 'p',
    title: 'Физика',
    tagline: 'По вашим конспектам: теория, формулы, анимации, тесты',
    icon: 'atom',
    storage: { user: 'fpk.user.v1', admin: 'fpk.admin.v1', pack: 'fpk.pack.cache.v1' },
    cloud: { admin: 'fpk/admin', user: (uid) => `data/users/${uid}/state` },
    exportKind: 'fizika-progress',
    webIsDefault: false,
    v: { src: 'конспект', ofSrc: 'конспекта', inSrc: 'в конспекте', toSrc: 'к конспекту', fromSrc: 'из конспекта', bySrc: 'по конспекту', allSections: 'Все разделы физики' },
  },
  math: {
    id: 'math',
    prefix: 'm',
    title: 'Математика',
    tagline: 'По порядку тем вашей книги, с открытыми источниками',
    icon: 'pi',
    storage: { user: 'utc.math.user.v1', admin: 'utc.math.admin.v1' },
    cloud: { admin: 'fpk/math', user: (uid) => `data/users/${uid}/math` },
    exportKind: 'utc-math-progress',
    webIsDefault: true,
    v: { src: 'книга', ofSrc: 'книги', inSrc: 'в книге', toSrc: 'к книге', fromSrc: 'из книги', bySrc: 'по книге', allSections: 'Все разделы математики' },
  },
};

export const SUBJECT_IDS: SubjectId[] = ['physics', 'math'];
export const subjectByPrefix = (p: string): SubjectId | null => (p === 'p' ? 'physics' : p === 'm' ? 'math' : null);
export const APP_TITLE = 'UTC Preparation';
