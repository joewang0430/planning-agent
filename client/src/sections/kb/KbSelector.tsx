"use client";

import React, { useEffect, useState } from "react";
import KnowledgeBaseCard from "@/components/kb/KnowledgeBaseCard";
import { fetchKbList } from "../../api/baseApi";
import { KnowledgeBaseCategory } from "@/data/contentTypes";

const mockSelected = [
    { name: "知识库A", type: "db" },
    { name: "知识库B", type: "db" },
    { name: "知识库C", type: "db" },
    { name: "文件X", type: "file" },
];


const KbSelector = () => {
    // 后端返回的知识库分类和文件
    const [kbList, setKbList] = useState<KnowledgeBaseCategory[]>([]);
    // 当前选中的标签（分类）
    const [activeTag, setActiveTag] = useState<string | null>(null);
    // 搜索框内容
    const [search, setSearch] = useState("");

    useEffect(() => {
        fetchKbList().then(list => {
            setKbList(list);
            // 默认选中“01_组织机构”
            if (list.some(cat => cat.category === "01_组织机构")) {
                setActiveTag("01_组织机构");
            } else if (list.length > 0) {
                setActiveTag(list[0].category);
            }
        }).catch(console.error);
    }, []);

    // tags 就是后端返回的所有分类
    const tags = kbList.map(cat => cat.category);

    // 当前展示的其它知识库（即选中分类下的所有文件，支持搜索过滤）
    const other = React.useMemo(() => {
        if (!activeTag) return [];
        const cat = kbList.find(c => c.category === activeTag);
        if (!cat) return [];
        // 搜索过滤
        if (search.trim()) {
            return cat.files.filter(file => file.name.toLowerCase().includes(search.trim().toLowerCase()));
        }
        return cat.files;
    }, [activeTag, kbList, search]);

    return (
        <div className="flex flex-row gap-6 w-full h-full">
            {/* 已调用知识库（mock） */}
            <div className="border border-plagt-blue-1 rounded-2xl p-6 bg-white flex flex-col min-h-[400px] max-h-[600px]" style={{width: '50%'}}>
                <div className="text-center text-lg font-semibold text-blue-700 mb-4">已调用知识库</div>
                <div className="flex flex-col gap-2 flex-1 mb-6 overflow-y-auto" style={{maxHeight: 400}}>
                    {mockSelected.map((kb, i) => (
                        <KnowledgeBaseCard key={i} name={kb.name} type={kb.type as any} selected />
                    ))}
                </div>
                <button className="mx-auto mt-auto px-8 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600">保存</button>
            </div>
            {/* 其它知识库（动态渲染） */}
            <div className="border border-plagt-blue-1 rounded-2xl p-6 bg-white flex flex-col min-h-[400px] max-h-[600px]" style={{width: '50%'}}>
                <div className="text-center text-lg font-semibold text-blue-700 mb-4">其它知识库</div>
                <div className="flex items-center gap-2 mb-4">
                    <span className="text-gray-500">
                        <svg width="18" height="18" fill="none"><path d="M8 14a6 6 0 1 1 0-12 6 6 0 0 1 0 12Zm5.293 1.707a1 1 0 0 1-1.414-1.414l3.5-3.5a1 1 0 0 1 1.414 1.414l-3.5 3.5Z" stroke="#888" strokeWidth="1.5"/></svg>
                    </span>
                    <input
                        className="flex-1 border rounded px-2 py-1 text-sm"
                        placeholder="输入搜索标签"
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                        disabled={!activeTag}
                    />
                </div>
                <div className="flex flex-wrap gap-2 mb-4">
                    {tags.map(tag => (
                        <button
                            key={tag}
                            className={`px-3 py-1 rounded-full border text-xs ${activeTag === tag ? "bg-blue-100 border-blue-400 text-blue-700" : "bg-gray-100 border-gray-300 text-gray-600"}`}
                            onClick={() => {
                                setActiveTag(tag);
                                setSearch(""); // 切换标签时清空搜索
                            }}
                        >
                            {tag}
                        </button>
                    ))}
                </div>
                <div className="grid grid-cols-2 gap-x-4 gap-y-2 flex-1 overflow-y-auto" style={{maxHeight: 400}}>
                    {other.length === 0 && activeTag ? (
                        <div className="col-span-2 text-gray-400 text-center py-8">暂无知识库文件</div>
                    ) : (
                        other.map((kb, i) => (
                            <KnowledgeBaseCard key={kb.name + i} name={kb.name} type="db" />
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default KbSelector;
