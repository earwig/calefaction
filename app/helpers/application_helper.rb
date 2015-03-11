module ApplicationHelper

  def get_title(title = '')
    base = 'Calefaction'  # TODO: replace with settings name thing
    title.empty? ? base : "#{title} : #{base}"
  end
end
