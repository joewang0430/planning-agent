import { KnowledgeBaseFile } from "@/data/contentTypes";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export const classifyTitle = async(title: string) => {
    const res = await fetch(`${API_BASE_URL}/api/classify_title`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
    });
    if (!res.ok) throw new Error('标题检测失败: generateApi.ts');
    return await res.json(); // { valid: boolean }
};

// TOSTRUCT
export const generateOutline = async(
    title: string,
    selectedKbList: KnowledgeBaseFile[]
) => {
    const res = await fetch(`${API_BASE_URL}/api/outline`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title,
            selectedKbList, // directy convey context select knowledgebase
        }),
    });
    if (!res.ok) throw new Error('生成大纲失败: generateApi.ts');
    return await res.json();
};

// TOSTRUCT
export const generateContent = async(
    title: string,
    outline: string,
    knowledgeBaseIds?: string[]
) => {
    const res = await fetch(`${API_BASE_URL}/api/content`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title,
            outline,
            knowledgeBaseIds,
        }),
    });
    if (!res.ok) throw new Error('生成内容失败: generateApi.ts');
    return await res.json();
};