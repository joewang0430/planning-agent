import { GenerateContentResponse } from "@/data/generateTypes";

interface ContentDisplayProps {
    content: GenerateContentResponse['content'];
}

const ContentDisplay = ({ content }: ContentDisplayProps) => {
    const contentOutline = content.content_outline;

    return (
        <div className="space-y-8 py-4">
            {contentOutline.map((section, i) => (
                <div key={i} className="space-y-4">
                    {/* 一级标题 */}
                    <h2 className="text-xl font-bold text-gray-900 border-b pb-2">
                        {section.title}
                    </h2>
                    
                    {/* 遍历二级标题和其内容 */}
                    {section.children?.map((child, j) => (
                        <div key={j} className="ml-4 space-y-2">
                            {/* 二级标题 */}
                            <h3 className="text-lg font-semibold text-gray-800">
                                {child.title}
                            </h3>
                            {/* 详细内容 (只读) */}
                            <div className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed">
                                {child.content}
                            </div>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default ContentDisplay;