const ProjectCounter = ({ count, selectedTag, setSelectedTag }) => {
  return (
    <div className="flex items-center justify-between">
      {selectedTag ? (
        <div>
          <div className="flex items-center justify-start ">
            <div>
              <svg
                className="w-8 h-8"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"
                ></path>
              </svg>
            </div>

            <div>
              {selectedTag} ({count})
            </div>

            <button
              onClick={() => {
                setSelectedTag("");
              }}
              className="text-purple-500 hover:text-purple-600 px-2 py-1"
            >
              <svg
                className="w-8 h-8"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div>Projects ({count}) </div>
        </div>
      )}
    </div>
  );
};

export default ProjectCounter;
