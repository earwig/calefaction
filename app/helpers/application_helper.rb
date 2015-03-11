module ApplicationHelper

  def get_title(title = '')
    base = 'Calefaction'
    title.empty? ? base : "#{title} : #{base}"
  end
end
