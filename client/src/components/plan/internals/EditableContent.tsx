"use client";

import React, { useState } from "react";
import EditableBlock from "./EditableBlock";

interface EditableContentProps {
    defaultValue: string;
    // interfaces for subsequent content modification and logic rewriting
    onChange?: (newContent: string) => void;
    onRewriteClick?: () => void;
}

const EditableContent = ({ defaultValue, onChange, onRewriteClick }: EditableContentProps) => {
    const [isHovering, setIsHovering] = useState(false);

    return (
        // Use relative positioning to provide positioning context for the internal absolute button
        <div 
            className="relative"
            onMouseEnter={() => setIsHovering(true)}
            onMouseLeave={() => setIsHovering(false)}
        >
            {/* Reuse the existing EditableBlock components to handle the editing logic */}
            <EditableBlock 
                defaultValue={defaultValue}
                onChange={onChange}
            />

            {/* When the mouse hovers over it, a "Rewrite Content" button is displayed in the upper right corner */}
            {isHovering && (
                <button
                    className="absolute top-2 right-2 bg-blue-500 text-white px-2 py-1 rounded shadow text-xs whitespace-nowrap"
                    onClick={onRewriteClick}
                >
                    重写内容
                </button>
            )}
        </div>
    );
};

export default EditableContent;