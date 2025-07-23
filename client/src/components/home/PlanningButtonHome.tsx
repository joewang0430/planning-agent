

const PlanningButtonHome = () => {
    return (
        <button
            className="text-2xl px-10 py-3 rounded-xl border-none shadow-md cursor-pointer ml-2 transition-colors bg-plagt-blue-1 hover:bg-plagt-blue-2 text-white"
            
            onClick={() => window.location.href = '/plan?title='}
        >
            生成规划 →
        </button>
    );
}

export default PlanningButtonHome;