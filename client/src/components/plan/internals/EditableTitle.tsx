"use client";

import React, { useState } from "react";
import EditableContent from "./EditableContent";

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

    return (
        <div
            className="relative group"
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
        >
            {/* editable content area */}
            <EditableContent
                defaultValue={defaultValue}
                onChange={onChange}
            />
            {/* when hovering, the "Rewrite Title" button is displayed */}
            {hover && (
                <button
                    className={`absolute -top-8 left-0 bg-blue-500 text-white px-2 py-1 rounded shadow text-xs`}
                >
                    重写标题
                </button>
            )}
        </div>
    );
};

export default EditableTitle;