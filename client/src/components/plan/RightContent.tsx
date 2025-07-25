const RightContent = () => (
    <div className="flex flex-col h-full min-h-0">
        <div className="flex-1 min-h-0">
            <div className="text-center mb-6">
                <h3 className="text-lg font-semibold text-blue-600">实时问答</h3>
            </div>
            <div className="bg-gray-50 rounded-lg p-4 mb-4 overflow-y-auto min-h-32 h-full">
                <div className="text-gray-500 text-sm text-center">
                    随时输入您想问的问题，包括查询资料、联系协调等......
                </div>
            </div>
        </div>
        <form className="mt-auto flex flex-wrap gap-2">
            <input 
                type="text" 
                placeholder="输入您的问题..."
                className="flex-1 min-w-[120px] border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500"
            />
            <button
                type="submit"
                className="flex-shrink-0 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors min-w-[60px]"
            >
                发送
            </button>
        </form>
    </div>
);

export default RightContent;