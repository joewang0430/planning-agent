"use client";

import { useRef, useEffect } from "react";

// editable component
const EditableBlock = ({
    defaultValue,
    onChange,
}: {
    defaultValue: string;
    onChange?: (value: string) => void;
}) => {
    const ref = useRef<HTMLDivElement>(null);

    // set the content and adaptive height
    useEffect(() => {
        if (ref.current) {
            ref.current.innerText = defaultValue || "";
            ref.current.style.height = "auto";
            ref.current.style.height = ref.current.scrollHeight + "px";
        }
    }, [defaultValue]);

    // adaptive height when inputting
    const handleInput = (e: React.FormEvent<HTMLDivElement>) => {
        const el = e.currentTarget;
        el.style.height = "auto";
        el.style.height = el.scrollHeight + "px";
        if (onChange) {
            onChange(el.innerText);
        }
    };

    return (
        <div
            ref={ref}
            contentEditable
            suppressContentEditableWarning
            className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed border border-gray-200 rounded p-3 min-h-[32px] focus:outline-blue-400 transition-all"
            style={{ overflow: "hidden" }}
            onInput={handleInput}
        />
    );
};


export default EditableBlock;