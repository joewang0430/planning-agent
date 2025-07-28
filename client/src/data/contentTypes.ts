
// outline
type OutlineSection = {
  title: string;
  children?: { title: string }[];
};
export type OutlineStruct = OutlineSection[];


// kb list
export interface KnowledgeBaseFile {
    name: string;
    type: string;
    category?: string;
};
export interface KnowledgeBaseCategory {
    category: string;
    files: KnowledgeBaseFile[];
};