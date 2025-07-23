const BaseButtonHome = ()=> {
    return (
        <button
          className="bg-white hover:bg-gray-100 text-gray-600 text-2xl px-10 py-3 rounded-xl border-none shadow-md cursor-pointer transition-colors duration-300"
          onClick={() => window.location.href = '/knowledge'}
        >
          我的知识库
        </button>
    );
};

export default BaseButtonHome;