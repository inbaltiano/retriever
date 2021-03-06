#retriever
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, correct_invalid_value

class main(Script):
    def __init__(self):
        Script.__init__(self,
                        name="Gulf of Maine intertidal density/cover (Ecological Archives 2008)",
                        description="Peter S. Petraitis, Harrison Liu, and Erika C. Rhile. 2008. Densities and cover data for intertidal organisms in the Gulf of Maine, USA, from 2003 to 2007. Ecology 89:588.",
                        shortname="Petraitis2008",
                        ref="http://www.esapubs.org/archive/ecol/E089/032/",
                        urls = {
                                "main": "http://www.esapubs.org/archive/ecol/E089/032/Succession_sampling_03-07_data.txt",
                               },
                        tables = {
                                  "main": Table("main",
                                                cleanup=Cleanup(correct_invalid_value,
                                                                nulls=[-999.9])),
                                  }
                        )

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        self.engine.download_file(self.urls["main"], "Succession_sampling_03-07_data_original.txt")
        data_path = self.engine.format_filename("Succession_sampling_03-07_data.txt")
        old_data = open(self.engine.find_file("Succession_sampling_03-07_data_original.txt"), 'rb')
        new_data = open(data_path, 'wb')

        line1 = old_data.readline()
        line2 = old_data.readline()
        newline = line1.replace("\n", "\t") + line2
        new_data.write(newline)

        for line in old_data:
            new_data.write(line)

        new_data.close()
        old_data.close()

        self.engine.auto_create_table(self.tables["main"],
                                      filename="Succession_sampling_03-07_data.txt")
        self.engine.insert_data_from_file(data_path)


SCRIPT = main()
