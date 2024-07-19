__doc__ = "Select all placed elements of a Category"
__title__ = "Of Category"

from pyrevit import revit, DB, forms

categoryList = revit.doc.Settings.Categories

selection = revit.get_selection()

categoryDictionary = {}

for category in categoryList:
	categoryName = category.Name
	if 'tag' not in categoryName.lower() and 'anal' not in categoryName.lower():
		categoryDictionary[categoryName] = category.Id

selectedCategoryList = forms.SelectFromList.show(
	sorted(categoryDictionary.keys()),
	title='Chose items to delete',
	width=500,
	height=650,
	multiselect=True
)

placedElements = []
for selectedCategory in selectedCategoryList:
	builtInCategory = categoryDictionary[selectedCategory]
	categoryCollector = [x for x in DB.FilteredElementCollector(revit.doc).OfCategoryId(builtInCategory).WhereElementIsNotElementType().ToElementIds()]
	placedElements += categoryCollector

selection.set_to(placedElements)