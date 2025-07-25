import React from "react";
import { OutlineStruct } from "@/data/contentTypes";
import EditableTitle from "./EditableTitle";

// OutlineEditor：render AI-returned JSON，every title used EditableTitle
interface OutlineEditorProps {
    outline: OutlineStruct;
}

const OutlineEditor = ({ outline }: OutlineEditorProps) => {
    return (
        <div className="space-y-6">
            {outline.map((section, i) => (
                <div key={i} className="space-y-3">
                    {/* title （一级标题）*/}
                    <EditableTitle defaultValue={section.title} />
                    {/* sub title（二级标题）*/}
                    {section.children?.map((child, j) => (
                        <div key={j} className="ml-8">
                            <EditableTitle defaultValue={child.title} isSub />
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default OutlineEditor;