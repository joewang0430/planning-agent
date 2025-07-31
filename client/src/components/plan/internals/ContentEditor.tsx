"use client";

import React, { useState, useEffect } from "react";
import { GenerateContentResponse } from "@/data/generateTypes";
import EditableContent from "./EditableContent";
import RewriteInput from "../RewriteInput"; //
import { rewriteContentParagraph } from "@/api/generateApi";

interface ContentEditorProps {
    initialContentData: GenerateContentResponse['content'];
    planTitle: string;
    policyContext: string;
}

// Define a type to track the target
type RewriteTarget = {
    sectionIndex: number;
    childIndex: number;
} | null;

const ContentEditor = ({ initialContentData, planTitle, policyContext }: ContentEditorProps) => {
    // State the content data for easy updates
    const [content, setContent] = useState(initialContentData);
    const [rewriteTarget, setRewriteTarget] = useState<RewriteTarget>(null);
    const [isLoading, setIsLoading] = useState(false);

    // When external data changes, synchronize the internal state
    useEffect(() => {
        setContent(initialContentData);
    }, [initialContentData]);

    // Implement the logic for API calls and content updates
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
                // Create a deep copy of the content to modify it safely
                const newContentOutline = JSON.parse(JSON.stringify(content.content_outline));
                newContentOutline[sectionIndex].children[childIndex].content = res.new_content;
                setContent({ ...content, content_outline: newContentOutline });
            }
        } catch (error) {
            console.error("重写内容失败:", error);
            alert("重写内容失败，请检查网络或联系管理员。");
        } finally {
            setIsLoading(false);
            setRewriteTarget(null); // Close the input box after completion
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
                            
                            {/* Above the content block, render the input box based on the conditions */}
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
                                // When clicking the button, set the paragraph you want to rewrite currently
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