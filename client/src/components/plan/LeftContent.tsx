import { GenerateOutlineResponse } from "@/data/generateTypes";
import React from "react";
import OutlineEditor from "./internals/OutlineEditor";
import outlineExample from "@/data/examples/outline.json";

interface LeftContentProps {
    loading: boolean;
    data: GenerateOutlineResponse | null;
}

const LeftContent = ({loading, data}: LeftContentProps) => (
    <div className="flex flex-col h-full min-h-0">
        {/* 顶部固定 */}
        <div>
            <div className="bg-blue-50 px-3 py-1 rounded text-sm text-blue-600 inline-block mb-4">
                已参考 4 个知识库
            </div>
            <button className="ml-3 text-blue-500 text-sm hover:underline">
                查看/编辑知识库 →
            </button>
        </div>
        {/* 中间可滚动区域 */}
        <div className="flex-1 min-h-0 overflow-y-auto py-2">
            <div className="space-y-6">
                {loading ? (
                    <div className="text-center py-8">
                        <div className="text-blue-500">正在生成中...</div>
                    </div>
                ) : data ? (
                    <OutlineEditor outline={outlineExample} />
                ) : (
                    <div className="text-center py-8 text-gray-500">
                        加载失败
                    </div>
                )}
            </div>
        </div>
        {/* 底部固定 */}
        <div className="mt-auto flex flex-wrap gap-2 justify-between items-center pt-4">
            <button className="flex-shrink-0 flex items-center text-gray-600 hover:text-gray-800 min-w-[80px]">
                重写大纲
            </button>
            <div className="flex flex-wrap gap-2">
                <button className="flex-shrink-0 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors min-w-[90px]">
                    撰写内容
                </button>
                <button className="flex-shrink-0 border border-gray-300 px-4 py-2 rounded hover:bg-gray-50 transition-colors min-w-[70px]">
                    下载
                </button>
            </div>
        </div>
    </div>
);

export default LeftContent;