import { OutlineStruct } from "./contentTypes";

// this is used for getting api response, not in the ui
export interface GenerateOutlineResponse {
    success: boolean;
    title: string;
    outline: string;
    policy: string;
};