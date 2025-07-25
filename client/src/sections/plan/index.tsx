"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState, useRef } from "react";
import { generateOutline } from '../../api/generateApi';
import { GenerateOutlineResponse } from "@/data/generateTypes";
import RightContent from "@/components/plan/RightContent";
import LeftContent from "@/components/plan/LeftContent";

export const Plan = () => {
    const searchParams = useSearchParams();
    const title = searchParams.get('title') || '';
    const [data, setData] = useState<GenerateOutlineResponse | null>(null);
    const [loading, setLoading] = useState(false);

    // Segmentation ratio status
    const [leftWidth, setLeftWidth] = useState(60); // default left 60%
    const [isDragging, setIsDragging] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (title) {
            setLoading(true);
            generateOutline(title)
                .then(res => {
                    setData(res);
                    setLoading(false);
                })
                .catch(err => {
                    console.error('(from Plan index.tsx) API 调用失败:', err);
                    setData(null);
                    setLoading(false);
                });
        }
    }, [title]);

    // dragging process function
    const handleMouseDown = () => setIsDragging(true);

    const handleMouseMove = (e: MouseEvent) => {
        if (!isDragging || !containerRef.current) return;
        const containerRect = containerRef.current.getBoundingClientRect();
        const containerWidth = containerRect.width;
        const mouseX = e.clientX - containerRect.left;
        const newLeftWidth = Math.min(Math.max((mouseX / containerWidth) * 100, 20), 80);
        setLeftWidth(newLeftWidth);
    };

    const handleMouseUp = () => setIsDragging(false);

    useEffect(() => {
        if (isDragging) {
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
        }
        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        };
    }, [isDragging]);

    return (
        <main className="h-screen flex flex-col bg-gray-50 p-6">
            <div className="text-center mb-8">
                <h1 className="text-2xl font-bold text-gray-800">
                    {title || "专项规划生成"}
                </h1>
            </div>
            {/* main content */}
            <div 
                ref={containerRef}
                className="w-full px-4 mx-auto hidden lg:flex gap-1 flex-1 min-h-0"
            >
                {/* left box */}
                <div 
                    className="bg-white rounded-lg border border-blue-200 p-6 shadow-sm flex flex-col h-full min-h-0"
                    style={{ width: `${leftWidth}%` }}
                >
                    <LeftContent loading={loading} data={data}/>
                </div>
                {/* drag dividing line */}
                <div 
                    className={`w-2 bg-gray-300 hover:bg-blue-400 cursor-col-resize flex items-center justify-center rounded transition-colors ${
                        isDragging ? 'bg-blue-500' : ''
                    }`}
                    onMouseDown={handleMouseDown}
                >
                    <div className="w-1 h-8 bg-white rounded opacity-70"></div>
                </div>
                {/* right box */}
                <div 
                    className="bg-white rounded-lg border border-blue-200 p-6 shadow-sm flex flex-col h-full min-h-0"
                    style={{ width: `${100 - leftWidth}%` }}
                >
                    <RightContent />
                </div>
            </div>
            {/* modile layout */}
            <div className="max-w-4xl mx-auto lg:hidden space-y-6 flex-1 min-h-0">
                <div className="bg-white rounded-lg border border-blue-200 p-6 shadow-sm flex flex-col h-[80vh] min-h-0">
                    <LeftContent loading={loading} data={data}/>
                </div>
                <div className="bg-white rounded-lg border border-blue-200 p-6 shadow-sm flex flex-col h-[80vh] min-h-0">
                    <RightContent />
                </div>
            </div>
        </main>
    );
};