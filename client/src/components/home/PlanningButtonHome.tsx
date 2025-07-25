import { useRouter } from 'next/navigation';
import { useState } from 'react';

interface PlanningButtonHomeProps {
    title: string;
};

const PlanningButtonHome = ({ title }: PlanningButtonHomeProps) => {
    const router = useRouter();
    const [tip, setTip] = useState('');

    const handleClick = () => {
        if (!title.trim()) {
            setTip('标题不能为空');
            // disapear in 2s
            setTimeout(() => setTip(''), 2000);
            return;
        }
        setTip('');
        router.push(`/plan?title=${encodeURIComponent(title)}`);
    };

    return (
        <div className="inline-block relative">
            <button
                className="text-2xl px-10 py-3 rounded-xl border-none shadow-md cursor-pointer ml-2 transition-colors bg-plagt-blue-1 hover:bg-plagt-blue-2 text-white transition-colors duration-300"
                onClick={handleClick}
            >
                生成规划 →
            </button>
            {tip && (
                <div className="absolute left-1/2 -translate-x-1/2 mt-2 px-4 py-2 bg-red-500 text-white text-sm rounded shadow z-10 min-w-[150px] text-center">
                    {tip}
                </div>
            )}
        </div>
    );
};

export default PlanningButtonHome;