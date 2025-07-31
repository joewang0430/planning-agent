"use client";

import React, { useState } from "react";
import EditableBlock from "./EditableBlock";

interface EditableContentProps {
    defaultValue: string;
    onChange?: (newContent: string) => void;
    onRewriteClick?: () => void;
}

const EditableContent = ({ defaultValue, onChange, onRewriteClick }: EditableContentProps) => {
    const [isHovering, setIsHovering] = useState(false);

    return (
        <div 
            className="relative"
            onMouseEnter={() => setIsHovering(true)}
            onMouseLeave={() => setIsHovering(false)}
        >
            <EditableBlock 
                defaultValue={defaultValue}
                onChange={onChange}
            />

            {/* Display the button only when hovering and there is a callback function */}
            {isHovering && onRewriteClick && (
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