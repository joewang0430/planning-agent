interface WriteContentBtnProps {
    onClick?: () => void;
}

const WriteContentBtn = ({ onClick }: WriteContentBtnProps) => {
    return (
        <button 
            onClick={onClick}
            className="flex-shrink-0 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors min-w-[90px]">
            撰写内容
        </button>
    )
};

export default WriteContentBtn;