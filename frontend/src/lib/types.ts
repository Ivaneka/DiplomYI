export interface AnswerModel {
  text: string;
  is_correct: boolean;
}

export interface QuestionModel {
  text: string;
  options: AnswerModel[];
}

export interface TestModel {
  title: string;
  description: string;
  material_ids: number[];
  questions: QuestionModel[];
}

export interface MaterialModel {
  title: string;
  content: string;
}

export interface MaterialModelWithID {
  id: number;
  title: string;
  content: string;
}

export interface AnswerModelWithID {
  id: number;
  text: string;
  is_correct: boolean;
}

export interface QuestionModelWithID {
  id: number;
  text: string;
  answers: AnswerModelWithID[];
}

export interface TestModelWithID {
  id: number;
  title: string;
  description: string;
  material_ids: number[];
  questions: QuestionModelWithID[];
}

export interface AttemptAnswer {
  question_id: number;
  answer_id: number;
}

export interface Attempt {
  test_id: number;
  attempt_answers: AttemptAnswer[];
}
