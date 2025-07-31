interface RewriteOutlineBtnProps {
    onClick: () => void;
    isLoading: boolean;
}

const RewriteOutlineBtn = ({ onClick, isLoading }: RewriteOutlineBtnProps) => {
    return (
        <button 
            className="flex-shrink-0 flex items-center text-gray-600 hover:text-gray-800 min-w-[80px] disabled:text-gray-400 disabled:cursor-not-allowed"
            onClick={onClick}
            disabled={isLoading} 
        >
            {isLoading ? "重写中..." : "重写大纲"}
        </button>
    )
};

export default RewriteOutlineBtn;