@load base/files/extract
@load base/files/hash

const block_size = 512;

event file_state_remove(f: fa_file)
	{
	local i = 0;
	while ( i < f$seen_bytes)
		{
		print md5_hash(f$bof_buffer[i:block_size]);
		i = i + block_size;
		}
	}
