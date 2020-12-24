#include <rabbit/space/htrans.h>
#include <rabbit/space/screw.h>
#include <rabbit/space/camera.h>
#include <rabbit/intersect.h>

#include <nos/print.h>

int main()
{
	auto camera_X_position = rabbit::htrans2<double> { 0, {0, 0} };
	auto camera_Y_position = rabbit::htrans2<double> { 0, {10, 0} };

	auto camera_X = rabbit::camera2<double> { 1, camera_X_position };
	auto camera_Y = rabbit::camera2<double> { 1, camera_Y_position };
	auto camera_model = rabbit::camera2<double> { 1, {0.01, {10, 0}} };

	auto A = linalg::vec<double, 2> { -15, 20};
	auto B = linalg::vec<double, 2> {15, 10};
	auto C = linalg::vec<double, 2> {13, 50};

	PRINT(camera_X.project(A));
	PRINT(camera_Y.project(A));

	PRINT(camera_X.project(B));
	PRINT(camera_Y.project(B));

	auto a = camera_X.project(A);
	auto b = camera_Y.project(A);

	auto c = camera_X.project(B);
	auto d = camera_Y.project(B);

	auto l1 = camera_X.line_of_image(a);
	auto l3 = camera_X.line_of_image(c);

	auto l2 = camera_Y.line_of_image(b);
	auto l4 = camera_Y.line_of_image(d);


	for (int i = 0; i < 100000; ++i)
	{
		auto b1 = camera_model.project(B);
		auto b2 = camera_Y.project(B);
		auto error_b = b2 - b1;

		auto a1 = camera_model.project(A);
		auto a2 = camera_Y.project(A);
		auto error_a = a2 - a1;

		auto c1 = camera_model.project(C);
		auto c2 = camera_Y.project(C);
		auto error_c = c2 - c1;

		auto AX = camera_model.trans.inverse().transform(A);
		auto BX = camera_model.trans.inverse().transform(B);
		auto CX = camera_model.trans.inverse().transform(C);

		//PRINT(AX);

		double a_delta_x = - error_a * 0.001;
		double b_delta_x = - error_b * 0.001;
		double c_delta_x = - error_c * 0.001;
		double a_delta_a =  error_a * 0.001;
		double b_delta_a =  error_b * 0.001;
		double c_delta_a =  error_c * 0.001;

		camera_model.trans =
		    camera_model.trans
		    *
		    rabbit::htrans2<double>
		{
			//0,
			a_delta_a + b_delta_a + c_delta_a,// + a_delta_a,
			//c_delta_a + a_delta_a + b_delta_a,
			{
				a_delta_x, //+ b_delta_x + c_delta_x, //+ a_delta_x,
				//0,
				0//+ a_delta_y
			//		c_delta_x + a_delta_x + b_delta_x,
			//		c_delta_y + b_delta_y + a_delta_y
				//0, 0
			}
		};

		PRINT(camera_model.trans);
		PRINT(error_a);
		PRINT(error_b);
		PRINT(error_c);

	}
	//PRINT(camera_Y.trans);
	//PRINT(camera_model.trans);
}