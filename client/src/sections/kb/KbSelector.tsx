"use client";

import React, { useEffect, useState } from "react";
import KnowledgeBaseCard from "@/components/kb/KnowledgeBaseCard";
import { fetchKbList, deleteKnowledgeBase } from "../../api/baseApi";
import { KnowledgeBaseCategory } from "@/data/contentTypes";
import { useKnowledgeBase } from "@/contexts/KnowledgeBaseContext";


const KbSelector = () => {
    // 后端返回的知识库分类和文件
    const [kbList, setKbList] = useState<KnowledgeBaseCategory[]>([]);
    // 当前选中的标签（分类）
    const [activeTag, setActiveTag] = useState<string | null>(null);
    // 搜索框内容
    const [search, setSearch] = useState("");
    // kb context operation, used for global kb management
    const { selectedKbList, addKb, removeKb } = useKnowledgeBase();
    // selected kb in right part: 所有知识库, currently, it only support select one once
    const [selectedOtherKbName, setSelectedOtherKbName] = useState<string | null>();
    // 左侧已调用知识库选中
    const [selectedLeftKbIdx, setSelectedLeftKbIdx] = useState<number | null>(null);

    useEffect(() => {
        fetchKbList().then(list => {
            setKbList(list);
            // 默认选中“01_组织机构”
            if (list.some((cat: KnowledgeBaseCategory) => cat.category === "01_组织机构")) {
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
        <div className="flex flex-col md:flex-row gap-6 w-full h-full">
            {/* 已调用知识库（mock） */}
            <div className="border border-plagt-blue-1 rounded-2xl p-6 bg-white flex flex-col min-h-[400px] max-h-[600px] w-full md:w-1/2">
                <div className="text-center text-lg font-semibold text-blue-700 mb-4">已调用知识库</div>
                <div className="grid grid-cols-2 gap-x-4 gap-y-2 overflow-y-auto pt-2 pb-2 px-2" style={{maxHeight: 400}}>
                    {selectedKbList.map((kb, i) => (
                        <div key={i}>
                            <KnowledgeBaseCard 
                                name={kb.name} 
                                type={kb.type === 'db' ? 'db' : 'file'}
                                status={selectedLeftKbIdx === i ? "selected" : "normal"}
                                onClick={() => setSelectedLeftKbIdx(i)} 
                                category={kb.category}
                            />
                        </div>
                    ))}
                </div>
                <div className="flex gap-4 justify-center mt-auto">
                    <button 
                        className={`px-6 py-2 rounded-lg font-medium ${selectedLeftKbIdx === null ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                        disabled={selectedLeftKbIdx === null}
                        onClick={async () => {
                            if (selectedLeftKbIdx !== null) {
                                const kb = selectedKbList[selectedLeftKbIdx];
                                if (kb.type === 'upload') {
                                    try {
                                        await deleteKnowledgeBase(kb.name);
                                    } catch (err) {
                                        console.error('后端文件删除失败', err);
                                    }
                                }
                                removeKb(kb.name);
                                setSelectedLeftKbIdx(null);
                            }
                        }}
                    >移除所选</button>
                    <button 
                        className={`px-6 py-2 rounded-lg font-medium ${selectedKbList.length === 0 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                        disabled={selectedKbList.length === 0}
                        onClick={async () => {
                            for (const kb of selectedKbList) {
                                if (kb.type === 'upload') {
                                    try {
                                        await deleteKnowledgeBase(kb.name);
                                    } catch (err) {
                                        console.error('后端文件删除失败', err);
                                    }
                                }
                                removeKb(kb.name);
                            }
                            setSelectedLeftKbIdx(null);
                        }}
                    >全部移除</button>
                </div>
            </div>
            {/* 其它知识库（动态渲染） */}
            <div className="border border-plagt-blue-1 rounded-2xl p-6 bg-white flex flex-col min-h-[400px] max-h-[600px] w-full md:w-1/2">
                <div className="text-center text-lg font-semibold text-blue-700 mb-4">所有知识库</div>
                <div className="mb-2">
                    <div className="flex items-center gap-2">
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
                    <div className="w-full mt-2 mb-4 overflow-x-auto" style={{scrollbarWidth: 'none'}}>
                        <div className="flex flex-row gap-2 min-w-max px-1" style={{msOverflowStyle: 'none'}}>
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
                    </div>
                </div>
                <div className="grid grid-cols-2 gap-x-4 gap-y-2 overflow-y-auto px-2 pt-2 pb-2 mb-4" style={{maxHeight: 400}}>
                    {other.length === 0 && activeTag ? (
                        <div className="col-span-2 text-gray-400 text-center py-8">暂无知识库文件</div>
                    ) : (
                        other.map((kb, i) => {
                            let status: "normal" | "selected" | "added" = "normal";
                            if (selectedKbList.some(item => item.name === kb.name)) {
                                status = "added";
                            } else if (selectedOtherKbName === kb.name) {
                                status = "selected";
                            }
                            return (
                                <KnowledgeBaseCard 
                                    key={kb.name + i} 
                                    name={kb.name} 
                                    type="db" 
                                    status={status}
                                    category={activeTag ?? undefined}
                                    onClick={() => {
                                        if (status === "added") return;
                                        setSelectedOtherKbName(kb.name);
                                    }}
                                />
                            );
                        })
                    )}
                </div>
                
                <div className="flex justify-center gap-4 mt-auto">
                    <button
                        className="px-8 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-300"
                        disabled={!selectedOtherKbName}
                        onClick={() => {
                            const kb = other.find(k => k.name === selectedOtherKbName);
                            if (kb) addKb(kb);
                            setSelectedOtherKbName(null);
                        }}
                    >
                        选择
                    </button>
                </div>
            </div>
        </div>
    );
};

export default KbSelector;
