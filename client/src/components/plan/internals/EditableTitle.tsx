"use client";

import React, { useState } from "react";
import EditableBlock from "./EditableBlock";
import RewriteInput from "../RewriteInput";

interface EditableTitleProps {
    defaultValue: string;
    onChange?: (value: string) => void;
    isSub?: boolean; // if is sub title
};

// show button when hovered
const EditableTitle = ({
    defaultValue,
    onChange,
    isSub = false,
}: EditableTitleProps) => {
    const [hover, setHover] = useState(false);
    const [isRewriteActive, setIsRewriteActive] = useState(false);

    const handleRewriteSubmit = (requirement: string) => {
        // TODO: 在下一步中将在这里调用API
        console.log("用户要求:", requirement);
        // 成功后关闭输入框
        // setIsRewriteActive(false); 
    };

    return (
        <div
            className="relative group"
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
        >
            {/* editable content area */}
            <EditableBlock
                defaultValue={defaultValue}
                onChange={onChange}
            />
            {/* when hovering, the "Rewrite Title" button is displayed */}
            {hover && (
                <button
                   className="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-500 text-white px-2 py-1 rounded shadow text-xs whitespace-nowrap"
                   onClick={() => setIsRewriteActive(true)}
                >
                    {isSub ? "重写标题" : "重写整段标题"}
                </button>
            )}
            {/* Render it when the input box is activated */}
            {isRewriteActive && (
                <RewriteInput
                    // TODO: 在下一步中实现真正的加载状态
                    isLoading={false} 
                    onSubmit={handleRewriteSubmit}
                    onClose={() => setIsRewriteActive(false)}
                />
            )}
        </div>
    );
};

// className="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-500 text-white px-2 py-1 rounded shadow text-xs" // ← 这里改定位

export default EditableTitle;