import { GenerateOutlineResponse } from "@/data/generateTypes";
import { useRef, useEffect } from "react";

interface LeftContentProps {
    loading: boolean;
    data: GenerateOutlineResponse | null;
}

// editable component
const EditableContent = ({
    defaultValue,
    onChange,
}: {
    defaultValue: string;
    onChange?: (value: string) => void;
}) => {
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (ref.current) {
            ref.current.innerText = defaultValue || "";
        }
    }, [defaultValue]);

    return (
        <div
            ref={ref}
            contentEditable
            suppressContentEditableWarning
            className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed border border-gray-200 rounded p-3 min-h-[120px] focus:outline-blue-400"
            onInput={e => {
                if (onChange) {
                    onChange((e.target as HTMLDivElement).innerText);
                }
            }}
        />
    );
};

const LeftContent = ({loading, data}: LeftContentProps) => (
    <div className="flex flex-col h-full min-h-0">
        <div className="flex-1 min-h-0">
            <div className="mb-4">
                <div className="bg-blue-50 px-3 py-1 rounded text-sm text-blue-600 inline-block mb-4">
                    已参考 4 个知识库
                </div>
                <button className="ml-3 text-blue-500 text-sm hover:underline">
                    查看/编辑知识库 →
                </button>
            </div>
            <div className="space-y-6">
                {/* AI生成内容区域，已改为可编辑 */}
                {loading ? (
                    <div className="text-center py-8">
                        <div className="text-blue-500">正在生成中...</div>
                    </div>
                ) : data ? (
                    <div className="space-y-4">
                        <h3 className="font-semibold text-gray-800">生成结果:</h3>
                        {/* 可编辑内容区域 */}
                        <EditableContent defaultValue={data.outline} />
                    </div>
                ) : (
                    <div className="text-center py-8 text-gray-500">
                        加载失败
                    </div>
                )}
            </div>
        </div>
        {/* 按钮区域 */}
        <div className="mt-auto flex flex-wrap gap-2 justify-between items-center pt-4 border-t">
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