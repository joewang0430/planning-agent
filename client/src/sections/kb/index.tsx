"use client";

import React, { useRef } from "react";
import KbSelector from "./KbSelector";
import { useRouter } from "next/navigation";
import { useKnowledgeBase } from "@/contexts/KnowledgeBaseContext";
import { uploadKnowledgeBase } from "@/api/baseApi";

const KnowledgeBase = () => {
  const router = useRouter();
  const { addKb } = useKnowledgeBase();
  const fileInputRef = useRef<HTMLInputElement>(null);
  return (
    <main className="h-screen flex flex-col bg-gray-50 p-6">
      <div className="flex items-center justify-between mb-6">
        <button 
          className="px-4 py-1 border border-blue-400 rounded-lg text-blue-700 bg-white hover:bg-blue-50"
          onClick={() => router.push("/")}
        >← 返回</button>
        <label className="px-6 py-2 border border-blue-400 rounded-lg text-blue-700 bg-white hover:bg-blue-50 font-medium cursor-pointer">
          上传文件
          <input 
            type="file" 
            accept=".pdf,.doc,.docx,.txt"
            multiple
            style={{ display: 'none' }}
            ref={fileInputRef}
            onChange={e => {
              const files = e.target.files;
              if (!files) return;
              Array.from(files).forEach(async file => {
                try {
                  await uploadKnowledgeBase(file);
                  addKb({ name: file.name, type: 'upload', category: '上传文件' });
                } catch (err) {
                  // TODO：错误处理
                  console.error('文件上传失败', err);
                }
              });
              e.target.value = '';
            }}
          />
        </label>
      </div>
      <div className="flex-1 flex flex-col">
        <KbSelector />
      </div>
    </main>
  );
};

export default KnowledgeBase;