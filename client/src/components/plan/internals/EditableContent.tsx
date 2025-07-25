
"use client";

import { useRef, useEffect } from "react";

// editable component
const EditableContent = ({
    defaultValue,
    onChange,
}: {
    defaultValue: string;
    onChange?: (value: string) => void;
}) => {
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (ref.current) {
            ref.current.innerText = defaultValue || "";
        }
    }, [defaultValue]);

    return (
        <div
            ref={ref}
            contentEditable
            suppressContentEditableWarning
            className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed border border-gray-200 rounded p-3 min-h-[120px] focus:outline-blue-400"
            onInput={e => {
                if (onChange) {
                    onChange((e.target as HTMLDivElement).innerText);
                }
            }}
        />
    );
};

export default EditableContent;