import { classifyTitle } from '@/api/generateApi';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

interface PlanningButtonHomeProps {
    title: string;
    setTitle: (t: string) => void;
};

const PlanningButtonHome = ({ title, setTitle }: PlanningButtonHomeProps) => {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);
    const [tip, setTip] = useState('');
    const [error, setError] = useState('');

    const handleClick = async() => {
        if (!title.trim()) {
            setTip('标题不能为空');
            // disapear in 2s
            setTimeout(() => setTip(''), 2000);
            return;
        }
        setTip('');
        setError('');
        setIsLoading(true);
        try {
            const res = await classifyTitle(title);
            if (res.valid) {
                router.push(`/plan?title=${encodeURIComponent(title)}`);
            } else {
                setError('标题无意义或不具体，请重新输入');
                setTitle(''); // clear imput bar
            }
        } catch {
            setError('标题检测失败，请稍后重试');
        }
        setIsLoading(false);
    };

    return (
        <div className="inline-block relative">
            <button
                className="text-2xl px-10 py-3 rounded-xl border-none shadow-md cursor-pointer ml-2 transition-colors bg-plagt-blue-1 hover:bg-plagt-blue-2 text-white transition-colors duration-300"
                onClick={handleClick}
                disabled={isLoading}
            >
                {isLoading ? "分析中..." : "生成规划 →"}
            </button>
            {tip && (
                <div className="absolute left-1/2 -translate-x-1/2 mt-2 px-4 py-2 bg-red-500 text-white text-sm rounded shadow z-10 min-w-[150px] text-center">
                    {tip}
                </div>
            )}
            {error && (
                <div className="absolute left-1/2 -translate-x-1/2 mt-2 px-4 py-2 bg-red-500 text-white text-sm rounded shadow z-10 min-w-[150px] text-center">
                    {error}
                </div>
            )}
        </div>
    );
};

export default PlanningButtonHome;