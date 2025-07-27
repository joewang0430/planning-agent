
import React from "react";
import KbSelector from "./KbSelector";

const KnowledgeBase = () => {
  return (
    <main className="h-screen flex flex-col bg-gray-50 p-6">
      <div className="flex items-center justify-between mb-6">
        <button className="px-4 py-1 border border-blue-400 rounded-lg text-blue-700 bg-white hover:bg-blue-50">← 返回</button>
        <button className="px-6 py-2 border border-blue-400 rounded-lg text-blue-700 bg-white hover:bg-blue-50 font-medium">上传文件</button>
      </div>
      <div className="flex-1 flex flex-col">
        <KbSelector />
      </div>
    </main>
  );
};

export default KnowledgeBase;