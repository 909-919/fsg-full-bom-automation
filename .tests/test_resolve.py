from bom_automation import resolve_assembly_label

print(resolve_assembly_label('gear box', ['Gearbox']))
print(resolve_assembly_label('Front Uprights', ['Front Uprights','Gearbox']))
