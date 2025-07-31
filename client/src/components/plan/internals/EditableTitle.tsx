"use client";

import React, { useState } from "react";
import EditableBlock from "./EditableBlock";
import RewriteInput from "../RewriteInput";
import { rewriteSection, rewriteSubtitle } from "@/api/generateApi";
import { OutlineStruct, OutlineSection } from "@/data/contentTypes";

interface EditableTitleProps {
    defaultValue: string;
    isSub: boolean;
    fullOutline: OutlineStruct;
    sectionIndex: number;
    childIndex?: number;
    onOutlineChange: (newOutline: OutlineStruct) => void;
    planTitle: string;
    policyContext: string;
};

const EditableTitle = (props: EditableTitleProps) => {
    const {
        defaultValue,
        isSub,
        fullOutline,
        sectionIndex,
        childIndex,
        onOutlineChange,
        planTitle,
        policyContext,
    } = props;

    const [hover, setHover] = useState(false);
    const [isRewriteActive, setIsRewriteActive] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const handleRewriteSubmit = async (user_requirement: string) => {
        setIsLoading(true);
        try {
            if (isSub && childIndex !== undefined) {
                const parentSection = fullOutline[sectionIndex];
                const res = await rewriteSubtitle(
                    planTitle,
                    fullOutline, // FIX: Pass directly, without wrapping in an array
                    parentSection.title,
                    defaultValue,
                    policyContext,
                    user_requirement
                );

                if (res && res.success && res.new_title) {
                    const newOutline = JSON.parse(JSON.stringify(fullOutline));
                    if (newOutline[sectionIndex] && newOutline[sectionIndex].children) {
                        newOutline[sectionIndex].children[childIndex].title = res.new_title;
                    }
                    onOutlineChange(newOutline);
                }
            } else {
                const sectionToRewrite = fullOutline[sectionIndex];
                const res = await rewriteSection(
                    planTitle,
                    fullOutline, // FIX: Pass directly
                    sectionToRewrite, // FIX: Pass the object directly, not in an array
                    policyContext,
                    user_requirement
                );

                if (res && res.success && res.new_section) {
                    const newOutline = [...fullOutline];
                    newOutline[sectionIndex] = res.new_section;
                    onOutlineChange(newOutline);
                }
            }
        } catch (error) {
            console.error("Failed to rewrite title:", error);
        } finally {
            setIsLoading(false);
            setIsRewriteActive(false);
        }
    };

    return (
        <div
            className="relative group"
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
        >
            <EditableBlock defaultValue={defaultValue} />
            {hover && !isRewriteActive && (
                <button
                   className="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-500 text-white px-2 py-1 rounded shadow text-xs whitespace-nowrap"
                   onClick={() => setIsRewriteActive(true)}
                >
                    {isSub ? "重写标题" : "重写整段标题"}
                </button>
            )}
            {isRewriteActive && (
                <div className="mt-2">
                    <RewriteInput
                        isLoading={isLoading} 
                        onSubmit={handleRewriteSubmit}
                        onClose={() => setIsRewriteActive(false)}
                    />
                </div>
            )}
        </div>
    );
};

export default EditableTitle;