"use client";

import React, { useState, useEffect } from "react";
import { GenerateContentResponse } from "@/data/generateTypes";
import EditableContent from "./EditableContent";
import RewriteInput from "../RewriteInput";
import { rewriteContentParagraph } from "@/api/generateApi";

interface ContentEditorProps {
    initialContentData: GenerateContentResponse['content'];
    planTitle: string;
    policyContext: string;
}

type RewriteTarget = {
    sectionIndex: number;
    childIndex: number;
} | null;

const ContentEditor = ({ initialContentData, planTitle, policyContext }: ContentEditorProps) => {
    // 内部状态，用于管理和编辑内容
    const [content, setContent] = useState(initialContentData);
    const [rewriteTarget, setRewriteTarget] = useState<RewriteTarget>(null);
    const [isLoading, setIsLoading] = useState(false);

    // 核心修复：使用 useEffect 同步外部传入的数据
    // 当 initialContentData 这个 prop 发生变化时（例如，在父组件中重写了全部内容），
    // 这个 effect 会被触发，从而更新组件的内部状态 content。
    useEffect(() => {
        setContent(initialContentData);
    }, [initialContentData]);

    const handleRewriteSubmit = async (user_requirement: string) => {
        if (!rewriteTarget) return;
        setIsLoading(true);

        const { sectionIndex, childIndex } = rewriteTarget;
        const section = content.content_outline[sectionIndex];
        const child = section.children?.[childIndex];

        if (!child) {
            setIsLoading(false);
            return;
        }

        try {
            const res = await rewriteContentParagraph(
                planTitle,
                section.title,
                child.title,
                child.content || "",
                policyContext,
                user_requirement
            );

            if (res && res.success) {
                const newContentOutline = JSON.parse(JSON.stringify(content.content_outline));
                newContentOutline[sectionIndex].children[childIndex].content = res.new_content;
                setContent({ ...content, content_outline: newContentOutline });
            }
        } catch (error) {
            console.error("重写内容失败:", error);
            alert("重写内容失败，请检查网络或联系管理员。");
        } finally {
            setIsLoading(false);
            setRewriteTarget(null);
        }
    };

    return (
        <div className="space-y-8 py-4">
            {content.content_outline.map((section, i) => (
                <div key={i} className="space-y-4">
                    <h2 className="text-xl font-bold text-gray-900 border-b pb-2">
                        {section.title}
                    </h2>
                    
                    {section.children?.map((child, j) => (
                        <div key={j} className="ml-4 space-y-2">
                            <h3 className="text-lg font-semibold text-gray-800">
                                {child.title}
                            </h3>
                            
                            {rewriteTarget && rewriteTarget.sectionIndex === i && rewriteTarget.childIndex === j && (
                                <div className="mb-2">
                                    <RewriteInput
                                        isLoading={isLoading}
                                        onSubmit={handleRewriteSubmit}
                                        onClose={() => setRewriteTarget(null)}
                                    />
                                </div>
                            )}

                            <EditableContent 
                                defaultValue={child.content || ""}
                                onRewriteClick={() => setRewriteTarget({ sectionIndex: i, childIndex: j })}
                            />
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default ContentEditor;