export type KBFileType = "db" | "file";

// outline
export type OutlineSection = {
  title: string;
  children?: { title: string }[];
};
export type OutlineStruct = OutlineSection[];


// kb list
export interface KnowledgeBaseFile {
    name: string;
    type: KBFileType;   // if type==db: then is .xml data; if type==file then is uploaded data
    category?: string;
};
export interface KnowledgeBaseCategory {
    category: string;
    files: KnowledgeBaseFile[];
};

export type PageMode = 'outline' | 'content'