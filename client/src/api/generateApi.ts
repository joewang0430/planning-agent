
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

// TOSTRUCT
export const generateOutline = async(title: string, knowledgeBaseIds?: string[]) => {
    const res = await fetch(`${API_BASE_URL}/api/outline`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title,
            // knowledgeBaseIds,   // user locked knowledge base
        }),
    });
    if (!res.ok) throw new Error('生成大纲失败: generateApi.ts');
    return await res.json();
};

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