function [] = createDataset(datasets_list)
    datasets_list_length = length(datasets_list);
    for i=3:datasets_list_length
        name_dataset = strcat('/',datasets_list(i).name);
        h5create('dataset.h5',name_dataset,[inf inf],'ChunkSize',[1 11025])
    end
end
