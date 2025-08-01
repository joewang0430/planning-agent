interface RewriteContentBtnProps {
    onClick: () => void;
    isLoading: boolean;
    disabled: boolean;
}

const RewriteContentBtn = ({ onClick, isLoading, disabled }: RewriteContentBtnProps) => {
    return (
        <button 
            onClick={onClick}
            disabled={disabled || isLoading}
            className="flex-shrink-0 flex items-center text-gray-600 hover:text-gray-800 min-w-[80px] disabled:opacity-50 disabled:cursor-not-allowed"
        >
            {isLoading ? "重写中..." : "重写内容"}
        </button>
    )
};

export default RewriteContentBtn;