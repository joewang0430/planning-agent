"use client";

import React, { useState } from "react";
import KnowledgeBaseCard from "@/components/kb/KnowledgeBaseCard";

const mockSelected = [
  { name: "知识库A", type: "db" },
  { name: "知识库B", type: "db" },
  { name: "知识库C", type: "db" },
  { name: "文件X", type: "file" },
];

const mockOther = [
  { name: "知识库D", type: "db" },
  { name: "知识库E", type: "db" },
  { name: "知识库F", type: "db" },
  { name: "知识库G", type: "db" },
  { name: "知识库H", type: "db" },
  { name: "知识库I", type: "db" },
];

const tags = ["综合政务", "经济管理", "国土能源", "农业农村", "工业交通"];

const KbSelector: React.FC = () => {
  const [selected, setSelected] = useState(mockSelected);
  const [other, setOther] = useState(mockOther);
  const [search, setSearch] = useState("");
  const [activeTag, setActiveTag] = useState<string | null>(null);

  return (
    <div className="flex flex-col lg:flex-row gap-6 w-full h-full">
      {/* 已调用知识库 */}
      <div className="flex-1 border rounded-2xl p-6 bg-white flex flex-col min-h-[400px]">
        <div className="text-center text-lg font-semibold text-blue-700 mb-4">已调用知识库</div>
        <div className="grid grid-cols-2 gap-4 flex-1 mb-6">
          {selected.map((kb, i) => (
            <KnowledgeBaseCard key={i} name={kb.name} type={kb.type as any} selected />
          ))}
        </div>
        <button className="mx-auto mt-auto px-8 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600">保存</button>
      </div>
      {/* 其它知识库 */}
      <div className="flex-1 border rounded-2xl p-6 bg-white flex flex-col min-h-[400px]">
        <div className="text-center text-lg font-semibold text-blue-700 mb-4">其它知识库</div>
        <div className="flex items-center gap-2 mb-4">
          <span className="text-gray-500"><svg width="18" height="18" fill="none"><path d="M8 14a6 6 0 1 1 0-12 6 6 0 0 1 0 12Zm5.293 1.707a1 1 0 0 1-1.414-1.414l3.5-3.5a1 1 0 0 1 1.414 1.414l-3.5 3.5Z" stroke="#888" strokeWidth="1.5"/></svg></span>
          <input className="flex-1 border rounded px-2 py-1 text-sm" placeholder="输入搜索标签" value={search} onChange={e => setSearch(e.target.value)} />
        </div>
        <div className="flex flex-wrap gap-2 mb-4">
          {tags.map(tag => (
            <button key={tag} className={`px-3 py-1 rounded-full border text-xs ${activeTag === tag ? "bg-blue-100 border-blue-400 text-blue-700" : "bg-gray-100 border-gray-300 text-gray-600"}`} onClick={() => setActiveTag(tag)}>{tag}</button>
          ))}
        </div>
        <div className="grid grid-cols-2 gap-4 flex-1 overflow-y-auto">
          {other.map((kb, i) => (
            <KnowledgeBaseCard key={i} name={kb.name} type={kb.type as any} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default KbSelector;
