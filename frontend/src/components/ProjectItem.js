const ProjectItem = ({
  item: { link, fullname, twitter_handle, github_handle, screenshot_url, avatar_url, tags },
  selectedTag,
  setSelectedTag,
}) => {
  const handleTagSelect = (e) => {
    setSelectedTag(e.currentTarget.getAttribute("value"));
  };

  return (
    <div className="flex flex-col items-center justify-start sm:w-1/2 md:w-1/3 lg:w-1/4">
      <div className="border border-gray-400 mx-1 sm:mx-2 my-4 sm:my-3 bg-white rounded-xl shadow-lg">
        <div className="border-b border-gray-400 ">
          <a
            href={link}
            target="_blank"
            rel="noopener noreferrer"
            className="flex flex-col items-center justify-center hover:bg-gray-300 "
          >
            <img className="w-full rounded-t-xl" src={screenshot_url} alt="screenshot" />
          </a>
        </div>

        <div className="px-4 py-2">
          <div className="flex items-center justify-start flex-wrap">
            <div className="flex-shrink-0">
              {avatar_url ? (
                <img className="w-8 rounded-full mr-1" src={avatar_url} alt="twitter avatar" />
              ) : (
                <svg
                  className="w-8 mr-1 text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
                    clipRule="evenodd"
                  />
                </svg>
              )}
            </div>

            <div className="text-2xl font-semibold">{fullname}</div>
          </div>

          <div className="my-1">
            <div className="flex flex-wrap items-center mt-2">
              {tags.map((tag) => {
                return (
                  <div
                    key={tag}
                    value={tag}
                    onClick={handleTagSelect}
                    className={`block cursor-pointer rounded-xl font-medium text-sm px-2 py-1 mr-2 mt-2
                      ${
                        selectedTag === tag
                          ? "bg-purple-300 hover:bg-purple-400"
                          : "bg-gray-200 hover:bg-gray-300"
                      }
                      `}
                  >
                    {tag}
                  </div>
                );
              })}
            </div>

            <div className="flex flex-wrap items-center justify-center space-x-4 mt-4 text-xs text-gray-500">
              {twitter_handle ? (
                <div>
                  <a
                    href={`https://twitter.com/${twitter_handle}`}
                    className="hover:underline"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Twitter
                  </a>
                </div>
              ) : (
                ""
              )}
              {github_handle ? (
                <div>
                  <a
                    href={`https://github.com/${github_handle}`}
                    className="hover:underline"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Github
                  </a>
                </div>
              ) : (
                ""
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectItem;
