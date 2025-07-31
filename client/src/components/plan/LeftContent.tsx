import { GenerateOutlineResponse } from "@/data/generateTypes";
import React from "react";
import OutlineEditor from "./internals/OutlineEditor";
import PolicyDisplay from "./PolicyDisplay";
import Link from "next/link"; // 引入 Link 组件

interface LeftContentProps {
    loading: boolean;
    data: GenerateOutlineResponse | null;
};

const LeftContent = ({loading, data}: LeftContentProps) => {
    return (
        <div className="flex flex-col h-full min-h-0">
            {/* Policy Display Section */}
            {data && data.policy && <PolicyDisplay policy={data.policy} kb_list={data.kb_list} />}

            {/* middle rollable */}
            <div className="flex-1 min-h-0 overflow-y-auto py-2">
                <div className="space-y-6">
                    {loading ? (
                        <div className="text-center py-8">
                            <div className="text-blue-500">正在生成中...</div>
                        </div>
                    ) : data ? (
                        <OutlineEditor outline={typeof data.outline === "string" ? JSON.parse(data.outline) : data.outline} />
                    ) : (
                        <div className="text-center py-8 text-gray-500">
                            加载失败
                        </div>
                    )}
                </div>
            </div>
            {/* button */}
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
};

export default LeftContent;