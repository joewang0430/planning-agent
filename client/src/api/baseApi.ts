const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export const fetchKbList = async() => {
    const res = await fetch(`${API_BASE_URL}/api/kb/list`);
    if (!res.ok) throw new Error("(from baseApi.ts)知识库列表获取失败");
    return await res.json();
};


export const uploadKnowledgeBase = async(file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE_URL}/api/kb/upload`, {
        method: 'POST',
        body: formData
    });
    if (!res.ok) throw new Error('(from baseApi.ts)知识库文件上传失败');
    return await res.json();
};

export const deleteKnowledgeBase = async(filename: string) => {
    const res = await fetch(`${API_BASE_URL}/api/kb/delete`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename })
    });
    if (!res.ok) throw new Error('(from baseApi.ts)知识库文件删除失败');
    return await res.json();
};