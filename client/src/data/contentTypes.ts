type OutlineSection = {
  title: string;
  children?: { title: string }[];
};

export type OutlineStruct = OutlineSection[];