import { useRouter } from 'next/navigation';

interface PlanningButtonHomeProps {
    title: string;
};

const PlanningButtonHome = ({title}: PlanningButtonHomeProps) => {
    const router = useRouter();
    return (
        <button
            className="text-2xl px-10 py-3 rounded-xl border-none shadow-md cursor-pointer ml-2 transition-colors bg-plagt-blue-1 hover:bg-plagt-blue-2 text-white transition-colors duration-300"
            onClick={() => router.push(`/plan?title=${encodeURIComponent(title)}`)}
        >
            生成规划 →
        </button>
    );
};

export default PlanningButtonHome;