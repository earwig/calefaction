module ApplicationHelper

  def get_title(title = '')
    base = '[Site Name]'
    title.empty? ? base : "#{title} : #{base}"
  end

  def get_copyright_year
    start = 2015
    year = Time.now.year
    year > start ? "#{start}–#{year}" : start
  end

  def get_project_version
    '0.1'  # todo
  end
end
