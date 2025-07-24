"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { generateOutline } from '../../api/generateApi';
import { GenerateOutlineResponse } from "@/data/generateTypes";

export const Plan = () => {
    const searchParams = useSearchParams();
    const title = searchParams.get('title') || '';
    const [data, setData] = useState<GenerateOutlineResponse | null>(null);
    const [loading, setLoading] = useState(false);

    // useEffect(() => {
    //     fetch(`${process.env.NEXT_PUBLIC_API_URL}/endpointTBD?title=${encodeURIComponent(title)}`)
    //         .then(res => res.json())
    //         .then(res => setData(res))
    //         .catch(() => setData(null))
    // }, [title]);
    useEffect(() => {
        if (title) {
            setLoading(true);
            generateOutline(title)// TOSTRUCT
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
    },[title])

    return (
        <>
            <h2>专项规划详情</h2>
            <div>标题: {title}</div>
            <div>
                {loading ? (
                    "正在生成中..."
                ) : data ? (
                    <>
                        <h3>生成结果:</h3>
                        <pre style={{whiteSpace: 'pre-wrap'}}>{data.outline}</pre>
                    </>
                ) : (
                    "加载失败"
                )}
            </div>
        </>
    );
};