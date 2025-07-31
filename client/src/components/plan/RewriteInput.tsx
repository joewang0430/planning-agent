"use client";

import { useState } from "react";


interface RewriteInputProps {
    onSubmit: (requirement: string) => void;
    onClose: () => void;
    isLoading: boolean;
}

const RewriteInput = ({ onSubmit, onClose, isLoading }: RewriteInputProps) => {
    const [requirement, setRequirement] = useState("");

    const handleSubmit = () => {
        if (isLoading) return;
        onSubmit(requirement);
    };

    return (
        <div className="mt-2 p-2 border border-blue-300 bg-blue-50 rounded-lg shadow-sm">
            <div className="flex items-center space-x-2">
                <input
                    type="text"
                    value={requirement}
                    onChange={(e) => setRequirement(e.target.value)}
                    placeholder="(可选) 提出重写要求"
                    className="flex-grow border border-gray-300 rounded px-2 py-1 text-sm focus:outline-blue-400"
                    onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
                />
                <button
                    onClick={handleSubmit}
                    disabled={isLoading}
                    className="bg-blue-500 text-white rounded px-3 py-1 text-sm font-semibold hover:bg-blue-600 disabled:bg-gray-400"
                >
                    {isLoading ? "..." : "▶"}
                </button>
                <button
                    onClick={onClose}
                    className="text-gray-500 hover:text-gray-800 font-bold text-lg"
                >
                    ✕
                </button>
            </div>
        </div>
    );
};

export default RewriteInput;