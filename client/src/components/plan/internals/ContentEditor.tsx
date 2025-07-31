import { GenerateContentResponse } from "@/data/generateTypes";
import EditableContent from "./EditableContent"; 

interface ContentEditorProps {
    content: GenerateContentResponse['content'];
}

const ContentEditor = ({ content }: ContentEditorProps) => {
    const contentOutline = content.content_outline;

    // 
    const handleContentChange = (newText: string, sectionIndex: number, childIndex: number) => {
        console.log(`内容变更于 [${sectionIndex}, ${childIndex}]:`, newText);
    };

    const handleRewriteClick = (sectionIndex: number, childIndex: number) => {
        console.log(`请求重写内容于 [${sectionIndex}, ${childIndex}]`);
    };

    return (
        <div className="space-y-8 py-4">
            {contentOutline.map((section, i) => (
                <div key={i} className="space-y-4">
                    {/* First-level headings (read-only) */}
                    <h2 className="text-xl font-bold text-gray-900 border-b pb-2">
                        {section.title}
                    </h2>
                    
                    {/* Traverse the secondary headings and their contents */}
                    {section.children?.map((child, j) => (
                        <div key={j} className="ml-4 space-y-2">
                            {/* Secondary headings (read-only) */}
                            <h3 className="text-lg font-semibold text-gray-800">
                                {child.title}
                            </h3>
                            
                            {/* Editable content blocks */}
                            <EditableContent 
                                defaultValue={child.content || ""}
                                onChange={(newText) => handleContentChange(newText, i, j)}
                                onRewriteClick={() => handleRewriteClick(i, j)}
                            />
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default ContentEditor;