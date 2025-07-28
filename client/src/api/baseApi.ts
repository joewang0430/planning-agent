const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export const fetchKbList = async() => {
    console.log("fe api called kb")
    const res = await fetch(`${API_BASE_URL}/api/kb/list`);
    if (!res.ok) throw new Error("(from baseApi.ts)知识库列表获取失败");
    return await res.json();
};

