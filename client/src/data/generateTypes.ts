import { OutlineStruct } from "./contentTypes";
import { KnowledgeBaseFile } from "./contentTypes";
import { generateContent } from '../api/generateApi';

// this is used for getting api response, not in the ui
export interface GenerateOutlineResponse {
    success: boolean;
    title: string;
    outline: string;
    policy: string;
    kb_list: KnowledgeBaseFile[];
};


// content
export interface ContentOutlineItem {
    title: string;
    children: {
        title: string;
        content: string;
    }[];
}

export interface GenerateContentResponse {
    success: boolean;
    title: string;
    content: {
        content_outline: ContentOutlineItem[];
    };
};